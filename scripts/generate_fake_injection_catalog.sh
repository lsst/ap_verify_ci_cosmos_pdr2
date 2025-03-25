SCRIPT_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
REPO_DIR="${SCRIPT_DIR}/../preloaded/"

print_error() {
    >&2 echo "$@"
}

usage() {
    print_error
    print_error "Usage: $0 [-b BUTLER_REPO] -o OUTPUT_COLLECTION [-h]"
    print_error
    print_error "Specific options:"
    print_error "   -b          Butler repo yaml file URI, defaults to preloaded repo"
    print_error "   -o          name of the output collection for injection catalog"
    print_error "   -h          show this message"
    exit 1
}

parse_args() {
    while getopts "b:o:h" option $@; do
        case "$option" in
            b)  BUTLER_REPO="$OPTARG";;
            o)  OUTPUT_COLLECTION="$OPTARG";;
            h)  usage;;
            *)  usage;;
        esac
    done
    if [[ -z "${BUTLER_REPO}" ]]; then
        BUTLER_REPO=$REPO_DIR
    fi
    if [[ -z "${OUTPUT_COLLECTION}" ]]; then
        print_error "$0: mandatory argument -- o"
        usage
        exit 1
    fi
}
parse_args $@

generate_injection_catalog \
    -a 149.3 151.2 \
    -d 1.4 2.95 \
    -m 21 28 \
    -i g r i \
    -p source_type Star \
    -s 5500 \
    -b ${BUTLER_REPO} \
    -w goodSeeingCoadd \
    -c 'templates/goodSeeing' \
    -o ${OUTPUT_COLLECTION} \
    --seed 314
