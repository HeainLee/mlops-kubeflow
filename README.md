# 🚀 Kubeflow Drift Detection & Retraining Pipeline (Azure AKS + KServe)

이 프로젝트는 Azure Kubernetes Service (AKS) 상에서 실행되는 Kubeflow 기반 MLOps 파이프라인 템플릿입니다.  
모델 학습 → 평가 → 조건부 배포(KServe) → 서빙 로그 기반 드리프트 감지 → 재학습 트리거까지 전 과정을 자동화합니다.

---

## 📁 프로젝트 구성

```
kubeflow-drift-retrain/
├── components/              # Kubeflow 컴포넌트 정의 (학습, 평가, 배포)
├── pipeline/                # 파이프라인 DSL 및 컴파일
├── monitoring/              # 드리프트 감지 및 트리거 스크립트
├── serving/                 # 커스텀 KServe 모델 서버 + Dockerfile + YAML
├── output/                  # 컴파일된 pipeline.yaml
├── logs/                    # 예측 로그 저장
├── requirements.txt
└── README.md
```

---

## ✅ 사전 준비 사항

- Azure AKS 클러스터
- Kubeflow Pipelines 설치
- KServe 설치
- PVC (model-pvc, log-pvc) 생성
- Azure Container Registry (ACR) 생성 및 로그인

---

## 🛠️ 설치 및 실행 순서

### 1. 컴포넌트 정의 및 파이프라인 컴파일
```bash
# 컴포넌트 정의 → YAML 생성
python components/train_component.py
python components/evaluate_component.py
python components/deploy_component.py

# 파이프라인 DSL → YAML 컴파일
python pipeline/compile_pipeline.py
```

---

### 2. KServe 커스텀 모델 서버 Docker 이미지 빌드 및 Push
```bash
cd serving
docker build -t <your-acr>/sklearn-kserve-logger:latest .
docker push <your-acr>/sklearn-kserve-logger:latest
```

※ `<your-acr>` 예시: `yourregistry.azurecr.io`

---

### 3. Kubeflow Pipeline 실행
- Kubeflow UI 또는 `kfp.Client()`를 통해 `output/pipeline.yaml`을 업로드 및 실행합니다.

---

### 4. 자동 InferenceService 배포 (deploy_component.py 내 자동 생성)
파이프라인 평가 단계에서 `"deploy"`로 판단되면 다음 YAML이 생성되어 `kubectl apply` 됩니다:

```yaml
apiVersion: serving.kubeflow.org/v1beta1
kind: InferenceService
metadata:
  name: iris-sklearn
spec:
  predictor:
    containers:
      - name: sklearn-custom
        image: yourregistry.azurecr.io/sklearn-kserve-logger:latest
        volumeMounts:
          - name: model-volume
            mountPath: /mnt/models
          - name: log-volume
            mountPath: /mnt/logs
    volumes:
      - name: model-volume
        persistentVolumeClaim:
          claimName: model-pvc
      - name: log-volume
        persistentVolumeClaim:
          claimName: log-pvc
```

---

### 5. 예측 요청 테스트 및 로그 확인
```bash
curl -X POST http://<EXTERNAL-IP>/v1/models/iris-sklearn:predict \
     -H "Content-Type: application/json" \
     -d '{"instances": [[5.1, 3.5, 1.4, 0.2]]}'
```

```bash
kubectl exec -it <POD_NAME> -- tail -f /mnt/logs/predict_log.json
```

---

### 6. 드리프트 감지 스크립트 실행
```bash
python monitoring/drift_detector.py
```

또는 주기 실행 (크론탭/워크플로우 등록)
```bash
crontab -e

# 매 시간마다 실행
0 * * * * /usr/bin/python3 /your/path/monitoring/drift_detector.py
```

---

## 📦 requirements.txt 패키지
```text
kfp==2.0.1
evidently==0.4.12
scikit-learn==1.2.2
joblib
pandas
kfserving
```

---

## 💡 확장 아이디어

| 기능 | 설명 |
|------|------|
| Katib 연동 | 자동 HPO 실험 가능 |
| Slack 알림 | 드리프트 발생 시 실시간 알림 |
| ArgoCD 연동 | InferenceService GitOps 관리 |
| Prometheus 연동 | 모델 모니터링 대시보드 구축 |

---

🔗 본 템플릿은 MLOps를 처음 시작하거나, Kubeflow-KServe 기반 CI/CD 파이프라인을 표준화하려는 팀에게 적합합니다.
