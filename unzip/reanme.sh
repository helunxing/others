# 遍历.zip
# for f in *.zip; do

# 遍历.livp
for f in *.livp; do

    # echo "${f%.zip}"
    # echo "$f"
    # echo "${f%.zip}.livp"
    # echo "to ${f%.livp}.zip"

    # .livp重命名到.zip
    mv "$f" "${f%.livp}.zip"

    # .zip重命名.livp
    # mv "$f" "${f%.zip}.livp"

    # 去除最后的.zip
    # mv "$f" "${f%.zip}"

    # 解压
    unzip -d output "${f%.livp}.zip"
    # unzip -d "${f%.zip}" "$f"

done
