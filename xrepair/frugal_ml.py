from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "xrepair_elm.joblib"

@dataclass
class Benchmark:
    accuracy: float
    train_seconds: float
    inference_ms_per_sample: float
    parameter_count: int

class ExtremeLearningMachine:
    """Single-hidden-layer Extreme Learning Machine.

    Hidden weights are randomly projected once; only the output layer is solved
    analytically by ridge-regularized least squares. This makes training fast and
    suitable for frugal/edge benchmarking.
    """
    def __init__(self, hidden_units=96, alpha=1e-3, random_state=17):
        self.hidden_units = int(hidden_units)
        self.alpha = float(alpha)
        self.random_state = int(random_state)
        self.scaler = StandardScaler()
        self.W = None
        self.b = None
        self.beta = None
        self.classes_ = None

    @staticmethod
    def _act(z):
        return np.tanh(z)

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y)
        Xs = self.scaler.fit_transform(X)
        self.classes_ = np.unique(y)
        class_to_i = {c:i for i,c in enumerate(self.classes_)}
        Y = np.zeros((len(y), len(self.classes_)))
        for i, label in enumerate(y):
            Y[i, class_to_i[label]] = 1.0

        rng = np.random.default_rng(self.random_state)
        self.W = rng.normal(0, 1/np.sqrt(max(Xs.shape[1],1)),
                            size=(Xs.shape[1], self.hidden_units))
        self.b = rng.uniform(-1, 1, size=(self.hidden_units,))
        H = self._act(Xs @ self.W + self.b)

        I = np.eye(self.hidden_units)
        self.beta = np.linalg.solve(H.T @ H + self.alpha * I, H.T @ Y)
        return self

    def decision_function(self, X):
        Xs = self.scaler.transform(np.asarray(X, float))
        H = self._act(Xs @ self.W + self.b)
        return H @ self.beta

    def predict_proba(self, X):
        z = self.decision_function(X)
        z = z - np.max(z, axis=1, keepdims=True)
        e = np.exp(z)
        return e / np.sum(e, axis=1, keepdims=True)

    def predict(self, X):
        p = self.predict_proba(X)
        return self.classes_[np.argmax(p, axis=1)]

    @property
    def parameter_count(self):
        if self.W is None:
            return 0
        return int(self.W.size + self.b.size + self.beta.size)

def save_elm(model, path=MODEL_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def load_elm(path=MODEL_PATH):
    return joblib.load(path) if path.exists() else None

def benchmark_model(model, X_train, y_train, X_test, y_test):
    t0 = time.perf_counter()
    model.fit(X_train, y_train)
    train_s = time.perf_counter() - t0

    t0 = time.perf_counter()
    pred = model.predict(X_test)
    infer_s = time.perf_counter() - t0

    return Benchmark(
        accuracy=float(accuracy_score(y_test, pred)),
        train_seconds=float(train_s),
        inference_ms_per_sample=float(1000*infer_s/max(len(X_test),1)),
        parameter_count=int(getattr(model, "parameter_count", 0)),
    )
