
document.addEventListener("DOMContentLoaded", function () {
  const formCliente = document.querySelector("#nuevoClienteModal form");

  if (formCliente) {
    formCliente.addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = new FormData(formCliente);
      const response = await fetch("/clientes/guardar-ajax", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        alert("Error en la solicitud");
        return;
      }

      const result = await response.json();

      if (result && result.id) {
        const clienteSelect = document.getElementById("cliente");
        const option = document.createElement("option");
        option.value = result.id;
        option.textContent = result.Nombre;

        // Agregar opción y seleccionarla
        clienteSelect.appendChild(option);
        clienteSelect.value = result.id;

        // Cerrar el modal
        const modalElement = document.getElementById('nuevoClienteModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
      } else {
        alert("Hubo un problema al registrar el cliente");
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const tabla = document.querySelector("#tablaProductos tbody");
  const agregarBtn = document.getElementById("agregarProducto");
  const productoSelect = document.getElementById("producto");
  const totalDisplay = document.getElementById("totalGeneral");

  function actualizarTotal() {
    let total = 0;
    tabla.querySelectorAll("tr").forEach(row => {
      const subtotal = parseFloat(row.querySelector(".subtotal").textContent.replace("$", ""));
      total += subtotal;
    });
    totalDisplay.textContent = $${ total.toFixed(2) };
  }

  function crearFilaProducto(nombre, precio, idProducto, stockDisponible) {
    const fila = document.createElement("tr");

    fila.innerHTML = 
        `<td>${nombre}</td>
        <td>$${precio.toFixed(2)}</td>
        <td>
            <input type="number" class="form-control cantidad-input" value="1" min="1" max="${stockDisponible}" style="width: 80px;">
            <small class="text-muted">Máx: ${stockDisponible}</small>
        </td>
        <td class="subtotal">$${precio.toFixed(2)}</td>
        <td>
            <button type="button" class="btn btn-danger btn-sm eliminar">Eliminar</button>
        </td>`
      ;

    const cantidadInput = fila.querySelector(".cantidad-input");

    // Validación al cambiar cantidad
    cantidadInput.addEventListener("input", function () {
      let cantidad = parseInt(this.value);

      if (cantidad > stockDisponible) {
        alert(No hay suficiente stock.Solo hay ${ stockDisponible } unidades disponibles.);
        this.value = stockDisponible;
        cantidad = stockDisponible;
      } else if (cantidad < 1) {
        this.value = 1;
        cantidad = 1;
      }
      const nuevoSubtotal = cantidad * precio;
      fila.querySelector(".subtotal").textContent = $${ nuevoSubtotal.toFixed(2) };
    });
    fila.querySelector(".eliminar").addEventListener("click", function () {
      fila.remove();
    });
    tabla.appendChild(fila);
  }


  agregarBtn.addEventListener("click", function () {
    const opcionSeleccionada = productoSelect.options[productoSelect.selectedIndex];
    const nombre = opcionSeleccionada.getAttribute("data-nombre");
    const precio = parseFloat(opcionSeleccionada.getAttribute("data-precio"));
    const stock = parseInt(opcionSeleccionada.getAttribute("data-stock"));
    const idProducto = opcionSeleccionada.value;

    crearFilaProducto(nombre, precio, idProducto, stock);
  });
});

function agregarSabor() {
  const container = document.getElementById("sabores-container");

  const div = document.createElement("div");
  div.className = "input-group mb-2";
  div.innerHTML = 
          `<div>
              <select name="id_Sabor[]" class="form-select sabor-select" required>
                  {% for sabor in sabores %}
                      <option value="{{ sabor.id_Sabor }}" data-nombre="{{ sabor.Nombre }}" data-precio="{{ sabor.Precio }}">
                          {{ sabor.Nombre }} - {{ sabor.Precio }}
                      </option>
                  {% endfor %}
              </select>
              <input type="number" name="Cantidad_Bolas[]" class="form-control bolas-input" placeholder="Bolas" min="1" required />
              <button type="button" class="btn btn-danger ms-1" onclick="this.closest('.input-group').remove()">
                  <i class="bi bi-trash"></i>
              </button>
          </div>`;
  container.appendChild(div);
}
function guardarHelado() {
  const sabores = document.querySelectorAll("#sabores-container .input-group");
  let nombreHelado = "";
  let precioTotal = 0;

  // Recorrer sabores seleccionados
  sabores.forEach(grupo => {
    const select = grupo.querySelector(".sabor-select");
    const inputBolas = grupo.querySelector(".bolas-input");

    const selectedOption = select.options[select.selectedIndex];
    const nombreSabor = selectedOption.getAttribute("data-nombre");
    const precioSabor = parseFloat(selectedOption.getAttribute("data-precio"));
    const bolas = parseInt(inputBolas.value || 1);

    if (!nombreSabor || isNaN(precioSabor) || isNaN(bolas)) return;

    const subtotal = precioSabor * bolas;
    nombreHelado += ${ nombreSabor } (${ bolas }), ;
  precioTotal += subtotal;
});

// Limpiar modal después de guardar
document.getElementById("sabores-container").innerHTML =`
  <div class="input-group mb-2">
    <select name="id_Sabor[]" class="form-select sabor-select" required>
      {% for sabor in sabores %}
      <option value="{{ sabor.id_Sabor }}" data-nombre="{{ sabor.Nombre }}" data-precio="{{ sabor.Precio }}">
        {{ sabor.Nombre }} - ${{ sabor.Precio }}
      </option>
      {% endfor %}
    </select>
    <input type="number" name="Cantidad_Bolas[]" class="form-control bolas-input" placeholder="Bolas" min="1" required />
    <button type="button" class="btn btn-danger ms-1" onclick="this.closest('.input-group').remove()">
      <i class="bi bi-trash"></i>
    </button>
  </div>
  `;

// Agregar a tabla de helados
const tablaHelados = document.querySelector("#tablaHelados tbody");

const fila = document.createElement("tr");
fila.innerHTML = `
        <td>${nombreHelado}</td>
        <td>$${precioTotal.toFixed(2)}</td>
        <td><input type="number" class="form-control cantidad-helado" value="1" min="1" style="width: 80px;"></td>
        <td class="subtotal-helado">$${precioTotal.toFixed(2)}</td>
        <td><button type="button" class="btn btn-danger btn-sm" onclick="this.closest('tr').remove(); actualizarTotales();">Eliminar</button></td>
  `
        ;

tablaHelados.appendChild(fila);

// Evento para cantidad
fila.querySelector(".cantidad-helado").addEventListener("input", function () {
  const cantidad = parseInt(this.value) || 1;
  const nuevoSubtotal = precioTotal * cantidad;
  fila.querySelector(".subtotal-helado").textContent = $${ nuevoSubtotal.toFixed(2) };
});

// Cerrar modal
bootstrap.Modal.getInstance(document.getElementById("heladoModal")).hide();

// Actualizar total general
setTimeout(actualizarTotales, 100);
    }


let totalProductos = 0;
let totalHelados = 0;

// Sumar productos fijos
document.querySelectorAll("#tablaProductos .subtotal").forEach(td => {
  const valor = parseFloat(td.textContent.replace("$", ""));
  if (!isNaN(valor)) totalProductos += valor;
});

// Sumar helados personalizados
document.querySelectorAll("#tablaHelados .subtotal-helado").forEach(td => {
  const valor = parseFloat(td.textContent.replace("$", ""));
  if (!isNaN(valor)) totalHelados += valor;
});

// Actualizar display por tabla
document.getElementById("totalProductos").textContent = $${ totalProductos.toFixed(2) };
document.getElementById("totalHelados").textContent = $${ totalHelados.toFixed(2) };

// Calcular total general
const totalVenta = totalProductos + totalHelados;
document.getElementById("totalGeneral").textContent = $${ totalVenta.toFixed(2) };
}

// Llama esta función cada vez que agregas un sabor
document.getElementById("agregarSaborBtn").addEventListener("click", function () {
  agregarSabor();
  setTimeout(actualizarSaboresDisponibles, 50);  // Esperar a que DOM actualice
});

// También llama cuando cambias un select
document.addEventListener("change", function (e) {
  if (e.target && e.target.classList.contains("sabor-select")) {
    actualizarSaboresDisponibles();
  }
});
