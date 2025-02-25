pkgname=easymanager
pkgver=1.0.8
pkgrel=1
arch=('x86_64')
pkgdesc="A standalone binary package containing easydots and easyscripts"
url="https://github.com/sumit6702/easymanager"
license=('MIT') # Change if needed
source=("easymanager.tar.xz")
sha256sums=('SKIP') # Replace with actual checksum if needed

package() {
    # Extract to package directory
    mkdir -p "$pkgdir/opt/easymanager"
    tar -xJf "$srcdir/easymanager.tar.xz" -C "$pkgdir/opt/easymanager"

    # Create symlinks for easy access
    install -Dm755 "$pkgdir/opt/easymanager/easydots/easydots" "$pkgdir/usr/bin/easydots"
    install -Dm755 "$pkgdir/opt/easymanager/easyscripts/easyscripts" "$pkgdir/usr/bin/easyscripts"
}
