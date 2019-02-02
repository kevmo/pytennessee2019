FROM fedora
# https://developers.cloudflare.com/argo-tunnel/downloads/
COPY cloudflared /usr/local/bin/cloudflared
ENTRYPOINT ["/usr/local/bin/cloudflared"]
CMD ["proxy-dns", "--address", "0.0.0.0"]
