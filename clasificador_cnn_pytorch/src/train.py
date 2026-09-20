import os
import sys

os.makedirs("output", exist_ok=True)

def entrenar_modelo(epochs=4, batch_size=32, lr=0.001):
    try:
        import torch
        import torch.nn as nn
        import torch.optim as optim
        from torch.utils.data import DataLoader
    except ImportError:
        print("\n" + "!" * 65)
        print("ℹ️ PyTorch no está instalado en este entorno virtual.")
        print("   Para entrenar la CNN, instala PyTorch:")
        print("     pip install torch torchvision")
        print("!" * 65 + "\n")
        return

    from model import SimpleCNN
    from dataset import generar_dataset_sintetico, ShapesDataset, guardar_muestras_individuales, CLASSES

    # Guardar muestras de prueba si no existen
    guardar_muestras_individuales()

    print("\n--- Generando dataset sintético de entrenamiento (Círculos, Cuadrados, Triángulos) ---")
    X_train, y_train, X_test, y_test = generar_dataset_sintetico(samples_per_class=200)

    train_dataset = ShapesDataset(X_train, y_train)
    test_dataset = ShapesDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
    print(f"Dispositivo de cómputo seleccionado: {device}")

    model = SimpleCNN(num_classes=len(CLASSES)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    print(f"\nIniciando entrenamiento por {epochs} épocas...")
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / total
        epoch_acc = (correct / total) * 100

        # Evaluación en test
        model.eval()
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                test_total += labels.size(0)
                test_correct += (predicted == labels).sum().item()

        test_acc = (test_correct / test_total) * 100
        print(f"Época [{epoch}/{epochs}] - Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc:.1f}% | Test Acc: {test_acc:.1f}%")

    model_path = "output/cnn_model.pth"
    torch.save(model.state_dict(), model_path)
    print(f"\n✅ Modelo entrenado guardado exitosamente en: {model_path}")

if __name__ == "__main__":
    entrenar_modelo()
