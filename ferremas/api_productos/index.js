const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const oracledb = require('oracledb');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// //////////////////////////////////////////////////
const dbConfig = {
  user: 'usuariosbd',
  password: 'usuariosbd',
  connectString: 'localhost:1521/orcl.duoc.com.cl' // o cambia orcl por el nombre correcto de tu servicio
};

// Obtener todos los productos///////////////////////////////
app.get('/productos', async (req, res) => {
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    const result = await connection.execute('SELECT * FROM productos');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Agregar producto al carrito
app.post('/carrito', async (req, res) => {
  const { usuario_id, producto_id, cantidad } = req.body;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (:usuario_id, :producto_id, :cantidad)`,
      { usuario_id, producto_id, cantidad },
      { autoCommit: true }
    );
    res.json({ msg: 'Producto agregado al carrito' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Obtener el carrito de un usuario
app.get('/carrito/:usuario_id', async (req, res) => {
  const { usuario_id } = req.params;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    const result = await connection.execute(
      `SELECT * FROM carrito WHERE usuario_id = :usuario_id`,
      { usuario_id }
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Actualizar la cantidad de un producto en el carrito
app.put('/carrito', async (req, res) => {
  const { usuario_id, producto_id, cantidad } = req.body;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `UPDATE carrito SET cantidad = :cantidad WHERE usuario_id = :usuario_id AND producto_id = :producto_id`,
      { cantidad, usuario_id, producto_id },
      { autoCommit: true }
    );
    res.json({ msg: 'Cantidad actualizada' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Eliminar un producto del carrito
app.delete('/carrito', async (req, res) => {
  const { usuario_id, producto_id } = req.body;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `DELETE FROM carrito WHERE usuario_id = :usuario_id AND producto_id = :producto_id`,
      { usuario_id, producto_id },
      { autoCommit: true }
    );
    res.json({ msg: 'Producto eliminado del carrito' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Actualizar producto
app.put('/productos/:id', async (req, res) => {
  const { id } = req.params;
  const { nombre, descripcion, precio, stock, categoria, marca, imagen } = req.body;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `UPDATE productos SET nombre=:nombre, descripcion=:descripcion, precio=:precio, stock=:stock, categoria=:categoria, marca=:marca, imagen=:imagen WHERE id=:id`,
      { nombre, descripcion, precio, stock, categoria, marca, imagen, id },
      { autoCommit: true }
    );
    res.json({ msg: 'Producto actualizado' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

// Eliminar producto
app.delete('/productos/:id', async (req, res) => {
  const { id } = req.params;
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `DELETE FROM productos WHERE id = :id`,
      { id },
      { autoCommit: true }
    );
    res.json({ msg: 'Producto eliminado' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

app.post('/productos', async (req, res) => {
  console.log(req.body);
  let { nombre, descripcion, precio, stock, categoria, marca, imagen } = req.body;
  // Convertir a número
  precio = parseFloat(precio);
  stock = parseInt(stock, 10);

  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    await connection.execute(
      `INSERT INTO productos (nombre, descripcion, precio, stock, categoria, marca, imagen)
       VALUES (:nombre, :descripcion, :precio, :stock, :categoria, :marca, :imagen)`,
      { nombre, descripcion, precio, stock, categoria, marca, imagen },
      { autoCommit: true }
    );
    res.json({ msg: 'Producto agregado' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  } finally {
    if (connection) await connection.close();
  }
});

app.get('/', (req, res) => {
  res.send('API de productos funcionando');
});

// Otros endpoints: actualizar/eliminar productos, ver carrito, etc.

// Iniciar servidor
const PORT = 3002;
app.listen(PORT, () => {
  console.log(`API de productos corriendo en http://localhost:${PORT}`);
});