FROM node:18

COPY . /app/frontend

RUN cd /app/frontend && npm install
# RUN npm run dev || true

WORKDIR /app/frontend

ENTRYPOINT ["npm", "run", "dev"]
