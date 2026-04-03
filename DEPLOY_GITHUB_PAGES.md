# GitHub Pages 发布说明

本项目的展示站点位于 `site/`，已经配置好 GitHub Pages 自动发布工作流。

## 你需要做的事

1. 在 GitHub 新建一个仓库。
2. 把当前项目推送到该仓库。
3. 在 GitHub 仓库中打开 `Settings -> Pages`。
4. 将 `Source` 设置为 `GitHub Actions`。
5. 向 `main` 或 `master` 分支推送后，GitHub 会自动发布 `site/` 目录。

## 发布后的访问地址

默认地址通常为：

`https://你的 GitHub 用户名.github.io/你的仓库名/`

例如仓库名为 `guozi-site`，用户名为 `example-user`，则地址为：

`https://example-user.github.io/guozi-site/`

## 本地没有 Git 时的可选方式

如果当前电脑没有安装 Git，可以用 GitHub Desktop：

1. 安装 GitHub Desktop。
2. 选择 `Add an Existing Repository from your Hard Drive`，导入当前项目目录。
3. 点击 `Publish repository`。
4. 回到 GitHub 网页端，把 Pages 的 Source 设为 `GitHub Actions`。

## 已完成的配置

- `.github/workflows/deploy-site.yml`：自动把 `site/` 发布到 GitHub Pages。
- `site/.nojekyll`：避免 GitHub Pages 对静态资源做 Jekyll 处理。

## 说明

站点当前使用相对路径资源引用，兼容 GitHub Pages 的仓库子路径部署，不需要额外修改前端路由或资源前缀。