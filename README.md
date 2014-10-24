XD-build core
=============

XD-build core contains the core infrastructure of the XD-build build system,
and should normally be the bottom layer of any XD-embedded manifest.

The intended scope for what should be included in XD-build core is to include
all the infrastructure for:

- Parsing XD-build recipes
- Executing XD-build recipes
- Related debug and development commands

It is not intended to be a home for important XD-build recipes, but might end
up including a few recipes which are essential for the above mentioned
infrastructure.

Other essential recipes should go in separate layers.  Toolchain related
recipes should be managed in an XD-build toolchain project.

## Developer resources

- Source code, issue tracking, website and wiki is hosted on
  [GitHub](https://github.com)
- [![Stories in Ready](https://badge.waffle.io/xd-embedded/xd-build-core.png?label=ready&title=Ready)](https://waffle.io/xd-embedded/xd-build-core) - Kanban board provided by [waffle.io](https://waffle.io/)
- [![Travis CI Status](https://travis-ci.org/XD-embedded/xd-build-core.svg?branch=master)](https://travis-ci.org/XD-embedded/xd-build-core) - Continous Integration is provided by [Travis CI](https://travis-ci.org)
- [![Coverage Status](https://coveralls.io/repos/XD-embedded/xd-build-core/badge.png?branch=master)](https://coveralls.io/r/XD-embedded/xd-build-core?branch=master) - Code coverage analysis is provided by [Coveralls](https://coveralls.io)
- [![Codacy Badge](https://www.codacy.com/project/badge/d52145a2b4c742518418ee90c3e295b6)](https://www.codacy.com/public/XD-embedded/xdbuildcore) - Static analysis is provided by [Codacy](https://www.codacy.com)
- [![Issue Stats](http://issuestats.com/github/XD-embedded/xd-build-core/badge/pr)](http://issuestats.com/github/XD-embedded/xd-build-core) [![Issue Stats](http://issuestats.com/github/XD-embedded/xd-build-core/badge/issue)](http://issuestats.com/github/XD-embedded/xd-build-core) - Issue and Pull Request statistics provided by [Issue Stats](http://issuestats.com/)

## License

XD-build core is released under the MIT License (see LICENSE file).
