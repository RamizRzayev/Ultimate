# Use the official Spark image as the base image
FROM docker.io/bitnami/spark:3

# Install BeautifulSoup4 and pymongo as root
USER root
RUN pip install beautifulsoup4 pymongo requests

# Switch back to a non-root user
USER 1001
