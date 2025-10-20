# Stage 1: build
FROM node:20-alpine AS build

WORKDIR /app

# Kopiujemy pliki package.json i package-lock.json
COPY package*.json ./

# Instalujemy wszystkie dependencies w tym devDependencies
RUN npm ci

# Kopiujemy resztę kodu
COPY . .

# Budujemy TS i Vite
RUN npx tsc -b && npx vite build

# Stage 2: produkcja z nginx
FROM nginx:alpine

# Kopiujemy statyczne pliki z build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Kopiujemy konfigurację nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
