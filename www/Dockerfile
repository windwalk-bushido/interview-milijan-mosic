# syntax=docker/dockerfile:1

# develop stage
FROM node:18-alpine as develop-stage
WORKDIR /www/container
COPY . /www/container
RUN rm -r node_modules
RUN npm install


# build stage
FROM develop-stage as build-stage
RUN npm run build


# production stage
FROM nginx:1.21.6-alpine as production-stage
COPY --from=build-stage /www/container/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=build-stage /www/container/default.conf /etc/nginx/conf.d/
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
