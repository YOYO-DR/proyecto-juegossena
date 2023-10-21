class modalBootstrap5 {
  constructor(title="",body="",footer="") {
    this.title,
    this.body,
    this.footer
  }
  plantillaElement() {
    
  }
}

const modalBootstrap5 = function () {
  let plantilla = `
  <div
  class="modal fade"
  id="modal"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body"></div>
    </div>
  </div>
</div>`;
  const modal = document.querySelector("#modal");
  const modalTitle = modal.querySelector(".modal-title");
  const modalBody = modal.querySelector(".modal-body");
}

document.addEventListener("DOMContentLoaded", (e) => {
  
})