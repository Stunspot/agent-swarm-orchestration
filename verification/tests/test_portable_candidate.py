import importlib.util,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools"))
import archive_paths as paths
import build_release as release
import build_candidate as candidate
import build_customer_kit as customer

class PortableCustodyTests(unittest.TestCase):
    def test_namespace_collisions_in_both_orders_and_valid_siblings(self):
        for entries in [[("src",b"a"),("src/a",b"b")],[("src/a",b"a"),("SRC",b"b")],[("A.txt",b"a"),("a.txt",b"b")]]:
            with self.assertRaises(ValueError):paths.check_members(entries)
        paths.check_members([("src/a",b"a"),("src/ab",b"b")])

    def test_invalid_names_and_long_budget_reject_before_final(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ["../escape","CON.txt","a./b","bad\\name","a:"+"x","a/"+"x"*220]:
                target=Path(d)/"out.zip"
                with self.assertRaises(ValueError):paths.atomic_zip([("first.txt",b"ok"),(name,b"bad")],target)
                self.assertFalse(target.exists())

    def test_write_failure_never_publishes_partial_archive(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"out.zip"
            original=zipfile.ZipFile.writestr;calls=[]
            def fail(z,*args,**kwargs):
                calls.append(1)
                if len(calls)==2:raise OSError("injected disk failure")
                return original(z,*args,**kwargs)
            with patch.object(zipfile.ZipFile,"writestr",fail):
                with self.assertRaises(OSError):paths.atomic_zip([("a",b"a"),("b",b"b")],target)
            self.assertFalse(target.exists())
            self.assertEqual([],list(Path(d).iterdir()))

    def test_existing_output_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"prior.zip";target.write_bytes(b"prior accepted bytes")
            with self.assertRaises(ValueError):paths.atomic_zip([("a",b"a")],target)
            self.assertEqual(b"prior accepted bytes",target.read_bytes())

    def test_actual_junction_source_member_and_target_ancestor(self):
        if os.name!="nt":self.skipTest("Windows junction control")
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);outside=base/"outside";outside.mkdir();(outside/"marker").write_bytes(b"outside")
            source=base/"source";source.mkdir();link=source/"linked"
            result=subprocess.run(["powershell","-NoProfile","-Command","New-Item -ItemType Junction -Path '"+str(link)+"' -Target '"+str(outside)+"' | Out-Null"],capture_output=True)
            if result.returncode:self.skipTest("junction unavailable")
            try:
                with self.assertRaises(ValueError):paths.assert_unlinked(source)
                with self.assertRaises(ValueError):paths.assert_unlinked(link)
                with self.assertRaises(ValueError):paths.atomic_zip([("a",b"a")],link/"output.zip")
                self.assertFalse((outside/"output.zip").exists())
            finally:os.rmdir(link)

    def test_candidate_preflight_failure_leaves_no_final_directory(self):
        with tempfile.TemporaryDirectory(dir=ROOT/"verification") as d:
            target=Path(d)/"candidate"
            with patch.object(customer,"preflight",side_effect=ValueError("late selected input invalid")):
                with self.assertRaises(ValueError):candidate.build(target)
            self.assertFalse(target.exists())

    def test_build_zip_outside_custody_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"source";source.mkdir();(source/"a").write_text("a")
            target=Path(d)/"outside.zip"
            with self.assertRaises(ValueError):release.build_zip(source,target,"skill")
            self.assertFalse(target.exists())

    def test_nested_archive_namespace_is_checked(self):
        import io
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,"w") as z:z.writestr("folder","a");z.writestr("folder/file","b")
        with self.assertRaises(ValueError):paths.check_members([("nested.zip",stream.getvalue())])

if __name__=="__main__":unittest.main()
