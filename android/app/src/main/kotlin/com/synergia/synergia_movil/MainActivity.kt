package com.synergia.synergia_movil

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.pm.PackageManager
import android.os.Build
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.OutputStream
import java.util.UUID
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.TimeoutException

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.synergia.synergia_movil/bluetooth_printer"
    private val SPP_UUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
    private val executor = Executors.newSingleThreadExecutor()

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "checkPermissions" -> {
                    result.success(hasBluetoothPermissions())
                }
                "getPairedDevices" -> {
                    val devices = getPairedDevicesList()
                    result.success(devices)
                }
                "printBytes" -> {
                    val address = call.argument<String>("address")
                    val bytes = call.argument<ByteArray>("bytes")

                    if (address.isNullOrBlank() || bytes == null || bytes.isEmpty()) {
                        result.error("INVALID_ARGS", "Dirección MAC o bytes vacíos", null)
                        return@setMethodCallHandler
                    }

                    executor.execute {
                        val success = printBytesOverBluetooth(address, bytes)
                        runOnUiThread {
                            result.success(success)
                        }
                    }
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private fun hasBluetoothPermissions(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            checkSelfPermission(android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED
        } else {
            checkSelfPermission(android.Manifest.permission.BLUETOOTH) == PackageManager.PERMISSION_GRANTED
        }
    }

    private fun getPairedDevicesList(): List<Map<String, String>> {
        val adapter = BluetoothAdapter.getDefaultAdapter() ?: return emptyList()
        if (!adapter.isEnabled) return emptyList()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
            checkSelfPermission(android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            return emptyList()
        }

        val list = mutableListOf<Map<String, String>>()
        val bondedDevices = adapter.bondedDevices ?: return emptyList()
        for (device in bondedDevices) {
            list.add(mapOf("name" to (device.name ?: "Impresora"), "address" to device.address))
        }
        return list
    }

    private fun printBytesOverBluetooth(address: String, bytes: ByteArray): Boolean {
        val adapter = BluetoothAdapter.getDefaultAdapter() ?: return false
        if (!adapter.isEnabled) return false

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
            checkSelfPermission(android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            return false
        }

        var socket: BluetoothSocket? = null
        var outputStream: OutputStream? = null

        return try {
            val device: BluetoothDevice = adapter.getRemoteDevice(address.uppercase().trim())

            // Cancelar descubrimiento si está activo para no degradar el ancho de banda
            adapter.cancelDiscovery()

            // Intento 1: Socket seguro estándar SPP
            var s: BluetoothSocket? = null
            try {
                s = device.createRfcommSocketToServiceRecord(SPP_UUID)
            } catch (e: Exception) {
                // Fallback: Socket inseguro para impresoras térmicas genéricas chinas
                s = device.createInsecureRfcommSocketToServiceRecord(SPP_UUID)
            }

            socket = s ?: return false

            // Conectar con timeout estricto de 3.5 segundos mediante sub-hilo
            val connectFuture = executor.submit {
                socket.connect()
            }

            try {
                connectFuture.get(3500, TimeUnit.MILLISECONDS)
            } catch (te: TimeoutException) {
                connectFuture.cancel(true)
                socket.close()
                return false
            }

            outputStream = socket.outputStream
            outputStream.write(bytes)
            outputStream.flush()

            // Esperar 150ms para drenado del búfer de cabezal térmico antes de cortar
            Thread.sleep(150)
            true
        } catch (e: Exception) {
            false
        } finally {
            try {
                outputStream?.close()
            } catch (_: Exception) {}
            try {
                socket?.close()
            } catch (_: Exception) {}
        }
    }
}
