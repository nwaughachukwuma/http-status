const jsonServer = require("json-server");

const server = jsonServer.create();
const router = jsonServer.router("db.json");
const middleware = jsonServer.defaults({
  readOnly: true,
});

const PORT = process.env.PORT || 3000;

server.use(middleware);

/** @type {jsonServer.JsonServerRouter} */
router.render = (req, res) => {
  const code = req.path.match(/^\/(\d+)/)?.[1];

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

server.get("/", (_req, res) => res.jsonp(router.db.value()));
server.use(router);
server.listen(PORT, () => {
  console.info(`Port:${PORT}`);
});

module.exports = server;
