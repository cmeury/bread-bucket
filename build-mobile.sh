#!/bin/bash
p4a apk --private /app \
    --package=com.bread.bucket \
    --name "Bread Bucket Mobile" \
    --version 0.1 \
    --bootstrap=webview \
    --requirements=flask,Flask-WTF,WTForms,Flask-SQLAlchemy,SQLAlchemy \
    --port=5000 \
    --dist_name BreadBucketMobile \
    --permission WRITE_EXTERNAL_STORAGE
mv /BreadBucketMobile*.apk /build/BreadBucketMobile.apk
