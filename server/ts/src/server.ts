import { fastify } from "fastify";
import { fastifyConnectPlugin } from "@connectrpc/connect-fastify";
import fastifyApiReference from "@scalar/fastify-api-reference";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import routes from "./connect.js";

async function main() {
  const server = fastify();
  await server.register(fastifyConnectPlugin, {
    routes,
  });
  server.get("/", (_, reply) => {
    reply.type("text/plain");
    reply.send("Hello World!");
  });

  // 提供 OpenAPI 文档
  server.get("/openapi.yaml", (_, reply) => {
    reply.type("application/yaml");
    const openapiPath = join(process.cwd(), "openapi.yaml");
    const content = readFileSync(openapiPath, "utf-8");
    reply.send(content);
  });

  server.register(fastifyApiReference, {
    routePrefix: "/reference",
    configuration: {
      title: "PetCode Server API 参考",
      url: "/openapi.yaml",
    },
  });

  // 从环境变量获取配置，默认值适合 Docker 部署
  const host = process.env.HOST || "0.0.0.0";
  const port = parseInt(process.env.PORT || "8080", 10);

  await server.listen({ host, port });
  console.log("server is listening at", server.addresses());
}

void main();
