# Maintainer: Your Name <your.email@example.com>
pkgname=easymanager
pkgver=1.0.8
pkgrel=1
pkgdesc="A simple manager for easydots and easyscripts"
arch=('x86_64')
url="https://github.com/sumit6702/easymanager"
license=('MIT')
source=("${url}/releases/download/v${pkgver}/easymanager.tar.xz")
sha256sums=('SKIP')

package() {
    cd "$srcdir"
    tar -xJf easymanager.tar.xz

    # Create directories in $pkgdir if they don't exist
    install -d "$pkgdir/usr/bin"
    install -d "$pkgdir/opt/easymanager/easydots"
    install -d "$pkgdir/opt/easymanager/easyscripts"

    cd "dist/easymanager"

    # Copy the directories into /opt, maintaining permissions and structure
    cp -r easydots "$pkgdir/opt/easymanager/"
    cp -r easyscripts "$pkgdir/opt/easymanager/"

    # Create symlinks in /usr/bin pointing to the binaries in /opt
    ln -s "/opt/easymanager/easydots/easydots.bin" "$pkgdir/usr/bin/easydots"
    ln -s "/opt/easymanager/easyscripts/easyscripts.bin" "$pkgdir/usr/bin/easyscripts"
}
