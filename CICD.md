```sh
[GitLab Push]
   ↓
[Jenkins CI] (소스 코드 테스트, 이미지 빌드)
   ↓
[Docker Registry] ← model_server 이미지 저장
   ↓
[GitOps Repo (infra 또는 k8s)] ← InferenceService, Pipeline YAML commit
   ↓
[ArgoCD] ← Git 변경 감지
   ↓
[Kubernetes + Kubeflow + KServe]
   ↳ Pipeline 실행
   ↳ 모델 서빙 배포
   ↳ 예측 로그 저장
   ↳ 드리프트 감지 → 재학습 트리거
```