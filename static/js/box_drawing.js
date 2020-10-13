// Bounding box drawing functions on top of images

function draw_box(ctx, lw, color, bbox) {
    ctx.lineWidth = lw;
    ctx.strokeStyle = color;
    ctx.strokeRect(bbox[0], bbox[1], bbox[2], bbox[3]);
}


function draw_boxes_on_canvas(cnv, info, wd, ht, type) {
    var ctx = cnv.getContext('2d');
    // set dashed if drawing a person detection
    if (type == 'pdet') {
        ctx.setLineDash([15, 10]);
        ctx.fillStyle = '#ffffff';
    }
    // draw each box
    for (var pid in info) {
        var bbox = [wd * info[pid].bbox[0], ht * info[pid].bbox[1],
                    wd * info[pid].bbox[2], ht * info[pid].bbox[3]];
        // draw black outer box for ground-truth
        if (type == 'gt') {
            draw_box(ctx, 5, '#000000', bbox);
        }
        if (type == 'pred') {
            draw_box(ctx, 5, '#FFFFFF', bbox);
        }
        // draw box
        draw_box(ctx, 3, info[pid].color, bbox);
        // check if confidence is there
        if ('conf' in info[pid]) {
            ctx.fillText(info[pid].conf.toString(), wd * info[pid].bbox[0], ht * info[pid].bbox[1]+10);
        }
    }
}
