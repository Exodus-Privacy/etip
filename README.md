<h1 align="center">ETIP - εxodus Tracker Investigation Platform</h1>

**ETIP** is meant to ease investigations on tracker detection. For the moment, it offers few features:

* Track all modifications on trackers
* Detect rules collisions for both network and code signature

The official instance of ETIP is available [here](https://etip.exodus-privacy.eu.org/).

<p align="center">
  <a href="https://github.com/Exodus-Privacy/etip/actions/workflows/main.yml">
    <img src="https://github.com/Exodus-Privacy/etip/actions/workflows/main.yml/badge.svg?branch=master" alt="Build Status"/>
  </a>
</p>

## Contributing

Please follow [Exodus Privacy's code of conduct](https://exodus-privacy.eu.org/en/page/coc/).

If you want to help us improve this project, you can:

- Use [issues](https://github.com/Exodus-Privacy/etip/issues) to report bugs and propose ideas or feature requests
- Join us on our [IRC channel #exodus-privacy on Libera.chat](https://web.libera.chat/?nick=webguest?#exodus-privacy)
- Refer to [this documentation](CONTRIBUTING.md) to improve the code.
- [Contribute to the identification of trackers](#contribute-to-the-identification-of-trackers)

### Contribute to the identification of trackers

If you wish to help us identify new trackers, you can **request an ETIP account** by sending a *username* and an *email address* to [etip@exodus-privacy.eu.org](mailto:etip@exodus-privacy.eu.org).

## Development environment

You have different ways of setting up your development environment (via Docker or manually), everything is explained [here](doc/install.md).

### Useful commands

Some admin commands are available to help administrate the ETIP database [here](doc/command.md).

## Administration API

An API is available to help administrate the ETIP database [here](doc/api.md).

## License

This project is licensed under the GNU AGPL v3 License - see the [LICENSE](LICENSE) file for details.

The ETIP database is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/.
