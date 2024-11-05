import React from 'react';

type ImageFile = {
    filename: string;
    base64: string;
};

type ImageGalleryProps = {
    folderName: string;
    images: ImageFile[];
};

const ImageGallery: React.FC<ImageGalleryProps> = ({ folderName, images }) => {
    return (
        <div style={{ marginBottom: '20px' }}>
            <h2>{folderName}</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {images.map((image, index) => (
                    <div key={index} style={{ textAlign: 'center' }}>
                        <img
                            src={image.base64}
                            alt={image.filename}
                            style={{ maxWidth: '200px', maxHeight: '200px' }}
                        />
                        <p>{image.filename}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ImageGallery;
