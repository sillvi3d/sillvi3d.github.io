---
title: Git 관련 명령어
---

## Push

변경사항을 GitHub에 올릴 때

```
cd D:\99_Obsidian\quartz
git add .
git commit -m "커밋 제목"
git push origin HEAD:main
```

---

## Pull 후 Push

push가 rejected 됐을 때 (원격에 내가 없는 커밋이 있을 때)

```
git pull origin main --rebase
git push origin HEAD:main
```

---

## 현재 상태 확인

어떤 파일이 변경됐는지 볼 때

```
git status
```

---

## 변경 내용 확인

어떤 내용이 바뀌었는지 볼 때

```
git diff
```

---

## 커밋 히스토리 확인

어떤 커밋들이 있는지 볼 때

```
git log --oneline
```

---

## 특정 파일 되돌리기

저장하기 전 파일을 마지막 커밋 상태로 되돌릴 때

```
git checkout -- 파일경로
```

---

## 마지막 커밋 취소 (파일은 유지)

커밋은 취소하되 변경사항은 남겨둘 때

```
git reset --soft HEAD~1
```

---

## 브랜치 확인

현재 어느 브랜치에 있는지 볼 때

```
git branch
```

---

## 원격 주소 확인

어느 GitHub 레포에 연결됐는지 볼 때

```
git remote -v
```

---

## 로컬 계정 설정 확인

현재 폴더의 git 계정 확인할 때

```
git config user.name
git config user.email
```

---

## 로컬 계정 설정 (폴더 단위)

특정 폴더에서만 다른 계정 쓸 때

```
git config user.name "sillvi3d"
git config user.email "sillvi3d@gmail.com"
```