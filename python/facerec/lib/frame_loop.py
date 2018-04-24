import cv2

def loop(frvideo, runtime_vars: dict, p_reg: dict):
    runtime_vars = p_reg.runtime_vars
    pipelines = p_reg.pipelines
    
    p_reg.hooks.on_start()

    while frvideo.capture.isOpened():
        # Grab a single frame of video
        ret, frame = frvideo.capture.read()
        if not ret:
            continue

        # handle frame flip
        if runtime_vars['flip_h']:
            frame = cv2.flip(frame, 0)
        if runtime_vars['flip_v']:
            frame = cv2.flip(frame, 1)

        # run the pipelines
        for _, pipeline in pipelines.items():
            if not pipeline.defer:
                pipeline.process(frame)
        
        c = cv2.waitKey(1)
        pipelines['key_press'].process(frame, c)

        if runtime_vars['quitting']:
            break

        # Display the resulting image in window
        if runtime_vars['window_enabled']:
            cv2.imshow(runtime_vars['window_name'], frame)

    p_reg.hooks.on_stop()
