document.addEventListener('DOMContentLoaded', function() {
  const userInfo = document.getElementById('user-info');
  const userModal = document.getElementById('user-modal');

  if (userInfo && userModal) {
    userInfo.addEventListener('click', function(event) {
      event.stopPropagation();
      if (userModal.style.display === 'block') {
        userModal.style.display = 'none';
      } else {
        userModal.style.display = 'block';
      }
    });
  }

  window.addEventListener('click', function(event) {
    if (userInfo && !userInfo.contains(event.target)) {
      userModal.style.display = 'none';
    }
  });
});
