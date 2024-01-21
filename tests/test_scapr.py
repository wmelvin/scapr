import scapr


def test_version():
    version = scapr.__version__
    assert isinstance(version, str), "Version should be a string"


def test_capture_to_output_dir(tmp_path):
    out_path = tmp_path / "output"
    out_path.mkdir()
    assert out_path.exists(), "Output folder should exist"
    args = [
        "--auto",
        "--folder",
        str(out_path),
        "--count",
        "2",
        "--seconds",
        "1",
    ]
    scapr.scap.main(args)
    assert len(list(out_path.glob("*.jpg"))) == 2, "Should have two files"
