FROM node:lts-alpine as dev

COPY package*.json ./

RUN npm ci

# make the 'app' folder the current working directory
WORKDIR /app


# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000
