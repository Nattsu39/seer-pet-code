# PetCode Server

## 项目描述

PetCode API v1 服务器实现，基于 TypeScript、Fastify 和 Connect RPC。

该 API 用于在不支持安装 SDK 的环境中序列化和反序列化 PetCodeMessage。提供 HTTP/JSON API 接口，支持将 PetCodeMessage 编码为 Base64 或从 Base64 解码为 PetCodeMessage。

项目链接：[seer-pet-code](https://github.com/nattsu39/seer-pet-code)

## 部署指南

### 方式一：使用 Docker 命令

#### 1. 运行容器

使用 petcode-server 镜像创建并启动容器：

```bash
docker run -d \
  --name petcode-server \
  -p 8080:8080 \
  -e NODE_ENV=production \
  -e HOST=0.0.0.0 \
  -e PORT=8080 \
  --restart unless-stopped \
  ghcr.io/nattsu39/petcode-ts-server:latest
```

#### 2. 查看日志

```bash
docker logs -f petcode-server
```

#### 3. 停止容器

```bash
docker stop petcode-server
```

#### 4. 启动已停止的容器

```bash
docker start petcode-server
```

#### 5. 删除容器

```bash
docker rm petcode-server
```

### 方式二：使用 Docker Compose（推荐）

#### 创建 docker-compose.yml 文件

在你的项目目录中创建 `docker-compose.yml` 文件，引用 petcode-server 镜像：

```yaml
version: '3.8'

services:
  petcode-server:
    image: ghcr.io/nattsu39/petcode-ts-server:latest
    container_name: my-petcode-server
    ports:
      - "3000:3000"  # 映射到主机的 3000 端口
    environment:
      - NODE_ENV=production
      - HOST=0.0.0.0
      - PORT=3000    # 容器内使用 3000 端口
    restart: unless-stopped
    networks:
      - my-network

networks:
  my-network:
    driver: bridge
```

#### 使用 Docker Compose 命令

1. **启动服务**

```bash
docker-compose up -d
```

1. **查看服务状态**

```bash
docker-compose ps
```

1. **查看日志**

```bash
docker-compose logs -f petcode-server
```

1. **停止服务**

```bash
docker-compose down
```

1. **重启服务**

```bash
docker-compose restart
```

### 配置说明

服务器支持以下环境变量配置：

| 变量名 | 说明 | 默认值 |
| -------- | ------ | -------- |
| `NODE_ENV` | 运行环境 | `production` |
| `HOST` | 监听地址 | `0.0.0.0` |
| `PORT` | 监听端口 | `8080` |

### 验证部署

部署成功后，访问以下 URL 验证服务是否正常运行：

```bash
curl http://localhost:8080/
```

预期输出：`Hello World!`
