# ---------- Build Stage ----------
# Use Node 18 Alpine image to build the React app
FROM node:18-alpine AS build

# Set working directory inside container
WORKDIR /app

# Copy only package.json files and install frontend dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy all frontend project files and build production files
COPY frontend/ ./
RUN npm run build


# ---------- Production Stage ----------
# Use Nginx to serve the built React app
FROM nginx:stable-alpine

# Copy build output from the build stage to Nginx's web root
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom Nginx config (if needed)
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Set correct permissions for static files
RUN chmod -R 755 /usr/share/nginx/html

# Expose port 80 so Nginx can serve content
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
