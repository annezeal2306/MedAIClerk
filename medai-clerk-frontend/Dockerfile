# --- Builder ---
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
# Install deps with whatever lockfile is present
RUN if [ -f pnpm-lock.yaml ]; then corepack enable && corepack prepare pnpm@latest --activate && pnpm i;         elif [ -f yarn.lock ]; then corepack enable && yarn install --frozen-lockfile;         elif [ -f package-lock.json ]; then npm ci;         else npm i; fi
COPY . .
ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
RUN npm run build

# --- Runner ---
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production         NEXT_TELEMETRY_DISABLED=1
# Copy only necessary output
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
# Next.js needs node_modules only for runtime server if not standalone; install prod deps
RUN npm i --omit=dev
EXPOSE 3000
CMD ["npm", "run", "start"]
