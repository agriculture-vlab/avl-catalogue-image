#!/usr/bin/env python3


import subprocess
from avl.catalogue import Catalogue


def main():

    print('Generating Markdown...')
    catalogue = Catalogue(
        dest_dir='/root/catalogue_markdown',
        max_datasets=3,
        use_stock_map=False,
        store_ids=['cciodp', 'ccizarr'],
        data_suffixes=['tif', 'tiff', 'zarr'],
    )
    catalogue.write_catalogue()

    print('Running mkdocs...')
    subprocess.run(
        ['mkdocs', 'build', '-f', '/root/mkdocs.yml'],
        cwd='/root'
    )

    print('Syncing...')
    subprocess.run(
        ['aws', 's3', 'sync', '.', 's3://agriculture-vlab-catalogue-test/',
         '--delete'],
        cwd='/root/catalogue_html'
    )


if __name__ == '__main__':
    main()
