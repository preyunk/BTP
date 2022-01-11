def updateBN(scale, model):
    for m in model.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.weight.grad.data.add_(scale*torch.sign(m.weight.data))  # L1