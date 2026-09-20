try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class SimpleCNN(nn.Module):
        """Red Neuronal Convolucional (CNN) simple para clasificación de imágenes de 32x32."""
        def __init__(self, num_classes=3):
            super(SimpleCNN, self).__init__()
            # Bloque Convolucional 1: (3, 32, 32) -> (32, 16, 16)
            self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

            # Bloque Convolucional 2: (32, 16, 16) -> (64, 8, 8)
            self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
            self.bn2 = nn.BatchNorm2d(64)
            self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

            # Clasificador Fully Connected: 64 * 8 * 8 = 4096
            self.fc1 = nn.Linear(64 * 8 * 8, 128)
            self.dropout = nn.Dropout(0.3)
            self.fc2 = nn.Linear(128, num_classes)

        def forward(self, x):
            # Bloque 1
            x = self.conv1(x)
            x = self.bn1(x)
            x = F.relu(x)
            x = self.pool1(x)

            # Bloque 2
            x = self.conv2(x)
            x = self.bn2(x)
            x = F.relu(x)
            x = self.pool2(x)

            # Aplanar
            x = torch.flatten(x, 1)

            # Capas densas
            x = self.fc1(x)
            x = F.relu(x)
            x = self.dropout(x)
            x = self.fc2(x)
            return x

except ImportError:
    class SimpleCNN:
        """Stub informativo en caso de que PyTorch aún no esté instalado en el entorno."""
        def __init__(self, num_classes=3):
            self.num_classes = num_classes
        def __repr__(self):
            return "SimpleCNN: Conv2d(3->32) -> MaxPool -> Conv2d(32->64) -> MaxPool -> Linear(4096->128) -> Linear(128->num_classes)"
