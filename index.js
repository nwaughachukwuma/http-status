const jsonServer = require("json-server");
const path = require("node:path");

const server = jsonServer.create();
const router = jsonServer.router(path.join(__dirname, "db.json"));
const middleware = jsonServer.defaults({
  readOnly: true,
});

const PORT = process.env.PORT || 3000;

server.use(middleware);

/** @type {jsonServer.JsonServerRouter} */
router.render = (req, res) => {
  const code = req.path.match(/^\/(\d+)/)?.[1];

  res.set("Cache-Control", "public, max-age=604800, immutable");

  if (!code) {
    res.status(400).jsonp("Bad Request. Use '/{status_code}'");
  } else if (!code.match(/^(\d{3})$/)) {
    res.status(406).jsonp("Not Acceptable");
  } else if (!router.db.get(code).value()) {
    res.status(501).jsonp("Not Implemented");
  } else {
    res.status(+code).jsonp(res.locals.data.code);
  }
};

server.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "public/index.html"));
});

server.get("/favicon.:ext", (_req, res) => {
  res.sendFile(path.join(__dirname, "public/favicon.ico"));
});

server.get("/favicon-:size.png", (req, res) => {
  res.sendFile(path.join(__dirname, `public/favicon-${req.params.size}.png`));
});

server.get("/codes", (_req, res) => res.jsonp(router.db.value()));
server.use(router);
server.listen(PORT, () => {
  console.info(`Port:${PORT}`);
});
