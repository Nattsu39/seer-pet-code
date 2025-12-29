# 多阶段构建 Dockerfile for PetCode Server

# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装所有依赖（包括 devDependencies）
RUN npm ci

# 复制源代码
COPY . .

# 构建 TypeScript 项目
RUN npm run build

# 生产阶段
FROM node:20-alpine AS production

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 仅安装生产依赖
RUN npm ci --omit=dev

# 从构建阶段复制编译后的文件
COPY --from=builder /app/dist ./dist

# 复制源代码（tsx 需要）
COPY --from=builder /app/src ./src

# 复制 OpenAPI 文档
COPY --from=builder /app/openapi.yaml ./openapi.yaml

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# 启动应用
CMD ["npm", "start"]

