# codespot/frontend/Dockerfile

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Vite usa el puerto 5173 por defecto
EXPOSE 5173

# Habilitamos el host para que sea accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host"]
