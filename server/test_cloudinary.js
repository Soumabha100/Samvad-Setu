const cloudinary = require('./src/config/cloudinary');
const streamifier = require('streamifier');

const testUpload = async () => {
  try {
    const buffer = Buffer.from("test image content", "utf8");
    const result = await new Promise((resolve, reject) => {
      const uploadStream = cloudinary.uploader.upload_stream(
        { folder: 'samvad_setu/problems' },
        (error, result) => {
          if (error) reject(error);
          else resolve(result);
        }
      );
      streamifier.createReadStream(buffer).pipe(uploadStream);
    });
    console.log("Success:", result.secure_url);
  } catch (error) {
    console.log("Cloudinary Error:", error.message || error);
  }
}

testUpload();
