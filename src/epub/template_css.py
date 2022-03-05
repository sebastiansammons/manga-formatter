stylesheet = """* {
    margin: 0;
    padding: 0;
}

img {
    height: [HEIGHT]px;
    width: [WIDTH]px;
    position: absolute;
    top: 0;
    z-index: -1;
    pointer-events: none;
}

img.right {
    left: 0;
}

img.left {
    right: 0;
}
"""
