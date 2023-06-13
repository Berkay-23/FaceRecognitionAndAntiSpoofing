const videoElement = $('#video')
const resolution = $('#overlay-bottom-right-text');
const btnLogin = $('#btnLogin');
const btnOpenModal = $('#btnOpenModal');
const btnRegister = $('#btnRegister');
const inpUsername = $('#username');

navigator.mediaDevices.getUserMedia({video: true})
    .then((stream) => {
        videoElement[0].srcObject = stream;
    })
    .catch((error) => {
        console.error('Kamera akışı alınamadı: ', error);
    });

videoElement.on('loadedmetadata', () => {
    resolution.text(videoElement[0].videoWidth + 'x' + videoElement[0].videoHeight);
});

btnLogin.on('click', () => {
    SendImage();
    showLoading('Yüz Verileri Kontrol Ediliyor', 'Lütfen bekleyiniz...');
    $.ajax({
        url: '/login',
        type: 'GET',
    }).done((data) => {
        let username = data.username;
        let message = data.message || null;

        if (message === null)
            showSwalAlert('Giriş Başarılı', `Hoşgeldin ${username}`, 'success');
        else
            showSwalAlert('Giriş Başarısız', message, 'error');

    });

});

btnRegister.on('click', () => {

    showLoading('Yüz Verileri Kaydediliyor', 'Lütfen bekleyiniz...');

    $.ajax({
        url: '/register',
        type: 'GET',
        data: {
            username: inpUsername.val()
        }
    }).done((data) => {
        let username = data.username;
        let message = data.message || null;

        if (message === null)
            showSwalAlert('Kayıt Başarılı', `Aramıza hoşgeldin ${username}`, 'success');
        else
            showSwalAlert('Kayıt Başarısız', message, 'error');

    });
    inpUsername.val('');
});

btnOpenModal.on('click', () => {
    SendImage();
    const photoRegister = $('img#photoRegister');
    const canvas = document.createElement('canvas');
    canvas.width = videoElement[0].videoWidth;
    canvas.height = videoElement[0].videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(videoElement[0], 0, 0, canvas.width, canvas.height);
    photoRegister.attr('src', canvas.toDataURL('image/jpeg', 1));
});

inpUsername.on('keyup', (event) => {
    if (event.keyCode === 13) {
        btnRegister.click();
    }
});

function SendImage() {
    let canvas = document.createElement('canvas');
    canvas.width = videoElement[0].videoWidth;
    canvas.height = videoElement[0].videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(videoElement[0], 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        // Blob verisini sunucuya göndermek için POST isteği yapın
        const formData = new FormData();
        formData.append('photo', blob, 'Berkay.jpg');

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                console.log('Image sent successfully to server');
            }
        };
        xhr.send(formData);
    }, 'image/jpeg', 1);
}

showSwalAlert = (title, text, icon) => {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'Tamam'
    });
}

showLoading = (title, text) => {
    Swal.fire({
        title: title,
        text: text,
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        },
    });
}