from xrepair.ml import train_model
if __name__=="__main__":
    _,acc=train_model()
    print(f"Modèle entraîné. Accuracy validation synthétique = {acc:.4f}")
