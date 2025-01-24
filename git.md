# Git 分支工作原理：并列分支与树状分支

## 假设场景：开发一个聊天应用
1. 项目分为 **前端** 和 **后端**。
2. 主分支是 `main`，用来保存稳定、可交付的代码。
3. 开发过程中，你的同学负责前端（`frontend` 分支），你负责后端（`backend` 分支）。

---

## 并列分支工作原理

### **1. 创建分支**
- 你的同学从 `main` 创建了 `frontend` 分支，你从 `main` 创建了 `backend` 分支：
  ```bash
  git checkout -b frontend
  git checkout -b backend
  ```

### **2. 分支开发**
- **你的同学**：在 `frontend` 分支中开发前端界面，提交代码。
  ```bash
  git add .
  git commit -m "Add chat interface"
  ```

- **你**：在 `backend` 分支中开发后端 API，提交代码。
  ```bash
  git add .
  git commit -m "Add chat API"
  ```

### **3. 合并到 `main`**
- 开发完成后，分别将 `frontend` 和 `backend` 合并到 `main`：
  ```bash
  # 合并 backend
  git checkout main
  git merge backend

  # 合并 frontend
  git merge frontend
  ```

### **4. 历史记录**
- 合并完成后，`main` 的提交历史看起来像这样（平行的分支）：
  ```
  A - Initial commit
  |\
  | B - Add chat API (backend)
  |/
  C - Add chat interface (frontend)
  ```

---

## 树状分支工作原理

### **1. 创建分支**
- 和并列分支一样，你和同学从 `main` 分别创建了 `frontend` 和 `backend` 分支。

### **2. 分支开发**
- **你的同学**：在 `frontend` 中开发前端界面之前，先同步 `main` 的最新代码：
  ```bash
  git checkout frontend
  git rebase main
  git add .
  git commit -m "Add chat interface"
  ```

- **你**：在 `backend` 中开发后端 API 之前，也同步 `main` 的最新代码：
  ```bash
  git checkout backend
  git rebase main
  git add .
  git commit -m "Add chat API"
  ```

### **3. 同步 `main` 更新**
- 如果 `main` 在开发期间有更新（例如修复了一个 Bug），你和同学需要同步到自己的分支：
  ```bash
  git checkout backend
  git rebase main
  ```

### **4. 合并到 `main`**
- 完成功能后，通过 Pull Request 或直接合并，提交到 `main`：
  ```bash
  git checkout main
  git merge backend
  git merge frontend
  ```

### **5. 历史记录**
- 合并完成后，`main` 的提交历史看起来更像树状结构：
  ```
  A - Initial commit
  |
  B - Add chat API (backend)
  |
  C - Add chat interface (frontend)
  ```

---

## 对比总结

### **并列分支**
- **优点**：分支互相独立，开发者之间无需频繁沟通。
- **缺点**：如果 `main` 更新，开发者需要手动处理冲突。

### **树状分支**
- **优点**：开发历史清晰，分支代码总是基于 `main` 最新状态。
- **缺点**：需要频繁同步 `main` 的更新，增加操作复杂度。

---



