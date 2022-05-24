**Note:** Commands tested on Linux

```
git clone https://github.com/windwalk-bushido/interview-milijan-mosic.git
```

Available on: http://127.0.0.1:8080

## Tech used

- Vue 3
- JavaScript
- Tailwind CSS
- Axios
- Python
- Flask
- Nginx
- Docker

# Task description:

The purpose of this series of tasks is to determine the ability to adapt to the unknown, apply known concepts, observing the candidate’s critical thinking and planning capabilities.

1. Create a project on GitHub with “interview-” as prefix and your full name kebab-case encoded as a suffix, for example: “interview-alice-jones”.

2. The project's goal is to create dockerized (Docker and docker-compose) dynamic To-do list web app. It is required to create dynamically multiple Todo items, also able to edit and mark them completed. There should be a client-side web app (frontend), and also a server-side (backend, API). The state is exchanged between client and server using fetch or Axios.

3. For the project, create a directory “www” for the frontend using React, Vue, Angular, Svelte, or a similar web library/framework. Use Materializecss and Material Design principles for UI/UX.

4. For the project, create directory “api” for backend using Node (Express.js), Python (Flask), Ruby (RoR), or technology of choice but not existing CMS. In the worst case, use JSON Server.

5. Use an HTTP server to bind the frontend and backend together, so issues with CORS are not present. The simplest way is to use Caddy v1, however Caddy v2, Nginx, and Apache are also viable options. Anyway, the candidate will need to write a configuration file and mount it in a docker container.

6. Write two individual “Dockerfile” files for frontend and backend.

7. Write “docker-compose.yml” that will start both frontend and backend with “docker-compose up --build”.

8. Allow project checking at http://127.0.0.1:8080
