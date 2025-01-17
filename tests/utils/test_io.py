from __future__ import annotations

import shutil

import torch

from matgl.utils.io import RemoteFile, get_available_pretrained_models, load_model


def test_remote_file():
    with RemoteFile(
        "https://github.com/materialsvirtuallab/matgl/raw/main/pretrained_models/MEGNet-MP-2018.6.1-Eform/model.pt",
        cache_location=".",
    ) as s:
        d = torch.load(s, map_location=torch.device("cpu"))
        assert "nblocks" in d["model"]["init_args"]
    try:  # cleanup
        shutil.rmtree("MEGNet-MP-2018.6.1-Eform")
    except FileNotFoundError:
        pass


def test_get_available_pretrained_models_load_model():
    model_names = get_available_pretrained_models()
    assert len(model_names) > 1
    assert "M3GNet-MP-2021.2.8-PES" in model_names
    model = load_model(model_names[0])
    assert issubclass(model.__class__, torch.nn.Module)
