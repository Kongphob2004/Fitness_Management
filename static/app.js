// ============================================================
//  app.js  —  ตรรกะหน้าเว็บ (ทำให้เสร็จแล้ว ★ นิสิตไม่ต้องแก้)
//  ปรับช่องค้นหา/ฟอร์มได้ที่ตัวแปร ENTITIES ด้านล่าง
// ============================================================
// ★ ตัวอย่าง dropdown ที่อ่านข้อมูลจากฐานข้อมูล: ฟอร์ม "การจอง" ช่อง class_id
//   แสดง name แต่ส่งค่าเป็น class_id (อ่านรายการจาก /api/classes)
//   ช่อง FK อื่น ๆ ทำแบบเดียวกันได้ — เปลี่ยน "type": "number" เป็น select + optionsFrom
const columnLabels = {
  member_id: "รหัสสมาชิก",
  name: "ชื่อสมาชิก",
  gender: "เพศ",
  phone: "เบอร์โทรศัพท์",
  join_date: "วันที่สมัครสมาชิก",
  package_type: "แพ็กเกจสมาชิก",

  trainer_id: "รหัสเทรนเนอร์",
  specialty: "ความเชี่ยวชาญ",

  class_id: "รหัสคลาส",
  room: "ห้องเรียน",
  schedule_time: "วันและเวลาเรียน",
  capacity: "จำนวนที่รับได้",
  seats_left: "จำนวนที่เหลือ",

  booking_id: "รหัสการจอง",
  booking_date: "วันที่จอง",
  status: "สถานะ",

  equip_id: "รหัสอุปกรณ์",
  zone: "โซน/พื้นที่",
  quantity: "จำนวนอุปกรณ์",

  checkin_id: "รหัส Check-in",
  member_name: "ชื่อสมาชิก",
  checkin_time: "เวลาเข้าใช้",
  checkout_time: "เวลาออก"
};

const entityColumnLabels = {
  members: {
    name: "ชื่อสมาชิก"
  },

  trainers: {
    name: "ชื่อเทรนเนอร์"
  },

  classes: {
    name: "ชื่อคลาส"
  },

  bookings: {
    name: "ชื่อสมาชิก"
  },

  equipment: {
    name: "ชื่ออุปกรณ์"
  },

  bookings: {
    status: "สถานะการจอง"
  },

  equipment: {
    status: "สถานะอุปกรณ์"
  }
};

const statusLabels = {
  booked: "จองแล้ว",
  cancelled: "ยกเลิกแล้ว",

  // สถานะอุปกรณ์
  available: "พร้อมใช้งาน",
  damaged: "ชำรุด"
};

const ENTITIES = {
  "members": {
    "label": "สมาชิก",
    "api": "/api/members",
    "idKey": "member_id",
    "search": [
      {
        "key": "name",
        "label": "ชื่อ",
        "type": "text"
      },
      {
        "key": "gender",
        "label": "เพศ",
        "type": "select",
        "options": [
          "",
          "Male",
          "Female",
          "Other"
        ]
      },
      {
        "key": "package_type",
        "label": "แพ็กเกจ",
        "type": "select",
        "options": [
          "",
          "Basic",
          "Premium"
        ]
      }
    ],
    "form": [
      {
        "key": "name",
        "label": "ชื่อ",
        "type": "text"
      },
      {
        "key": "phone",
        "label": "เบอร์โทรศัพท์",
        "type": "text"
      },
      {
        "key": "gender",
        "label": "เพศ",
        "type": "select",
        "options": [
          "Male",
          "Female",
          "Other"
        ]
      },
      {
        "key": "join_date",
        "label": "วันที่สมัคร",
        "type": "date"
      },
      {
        "key": "package_type",
        "label": "แพ็กเกจ",
        "type": "select",
        "options": [
          "Basic",
          "Premium"
        ]
      }
    ]
  },
  "trainers": {
  "label": "เทรนเนอร์",
  "api": "/api/trainers",
  "idKey": "trainer_id",

  "search": [
    {
      "key": "name",
      "label": "ชื่อเทรนเนอร์",
      "type": "text"
    },
    {
      "key": "specialty",
      "label": "ความเชี่ยวชาญ",
      "type": "select",
      "optionsFrom": {
        "api": "/api/trainers/specialties",
        "value": "specialty",
        "label": "specialty"
      }
    }
  ],

  "form": [
    {
      "key": "name",
      "label": "ชื่อเทรนเนอร์",
      "type": "text"
    },
    {
      "key": "phone",
      "label": "เบอร์โทรศัพท์",
      "type": "text"
    },
    {
      "key": "specialty",
      "label": "ความเชี่ยวชาญ",
      "type": "text"
    }
  ]
},
  "classes": {
    "label": "คลาสเรียน",
    "api": "/api/classes",
    "idKey": "class_id",
    "search": [
      {
        "key": "name",
        "label": "ชื่อคลาส",
        "type": "text"
      },
      {
        "key": "room",
        "label": "ห้อง",
        "type": "select",
          "optionsFrom": {
            "api": "/api/classes/rooms",
            "value": "room",
            "label": "room"
          }
      },
    ],
    "form": [
      {
        "key": "name",
        "label": "ชื่อคลาส",
        "type": "text"
      },
      {
        "key": "trainer_id",
        "label": "รหัสเทรนเนอร์",
        "type": "select",
        "optionsFrom" : {
          "api" : "/api/trainers",
          "value" : "trainer_id",
          "label" : "trainer_id"
        }
      },
      {
        "key": "room",
        "label": "ห้อง",
        "type": "text"
      },
      {
        "key": "capacity",
        "label": "จำนวนรับ",
        "type": "number"
      },
      {
        "key": "schedule_time",
        "label": "เวลา",
        "type": "datetime-local"
      }
    ]
  },
  "equipment": {
  "label": "อุปกรณ์",
  "api": "/api/equipment",
  "idKey": "equip_id",

  "search": [
    {
      "key": "name",
      "label": "ชื่ออุปกรณ์",
      "type": "text"
    },
    {
      "key": "zone",
      "label": "โซน",
      "type": "select",
      "optionsFrom": {
        "api": "/api/equipment/zones",
        "value": "zone",
        "label": "zone"
      }
    },
    {
      "key": "status",
      "label": "สถานะ",
      "type": "select",
      "options": [
        {
          "value": "",
          "label": "ทั้งหมด"
        },
        {
          "value": "available",
          "label": "พร้อมใช้งาน"
        },
        {
          "value": "damaged",
          "label": "ชำรุด"
        }
      ]
    }
  ],

  "form": [
    {
      "key": "name",
      "label": "ชื่ออุปกรณ์",
      "type": "text"
    },
    {
      "key": "zone",
      "label": "โซน",
      "type": "text"
    },
    {
      "key": "quantity",
      "label": "จำนวนทั้งหมด",
      "type": "number"
    },
    {
      "key": "status",
      "label": "สถานะ",
      "type": "select",
      "options": [
        {
          "value": "available",
          "label": "พร้อมใช้งาน"
        },
        {
          "value": "damaged",
          "label": "ชำรุด"
        }
      ]
    }
  ]
},
  "bookings": {
    "label": "การจอง",
    "api": "/api/bookings",
    "idKey": "booking_id",
    "search": [
      {
        "key": "member_id",
        "label": "รหัสสมาชิก",
        "type": "number"
      },
      {
        "key": "class_id",
        "label": "รหัสคลาส",
        "type": "number"
      },
      {
        "key": "status",
        "label": "สถานะ",
        "type": "select",
        "options": [
          "",
          {"value": "booked", "label": "จองแล้ว"},
          {"value": "cancelled", "label": "ยกเลิกแล้ว"},
        ]
      }
    ],
    "form": [
      {
        "key": "member_id",
        "label": "รหัสสมาชิก",
        "type": "number"
      },
      {
        "key": "class_id",
        "label": "คลาส",
        "type": "select",
        "optionsFrom": {
          "api": "/api/classes",
          "value": "class_id",
          "label": "name"
        }
      },
      {
        "key": "booking_date",
        "label": "วันที่จอง",
        "type": "date"
      },
      {
        "key": "status",
        "label": "สถานะ",
        "type": "select",
        "options": [
          {"value": "booked", "label": "จองแล้ว"},
          {"value": "cancelled", "label": "ยกเลิกแล้ว"},
        ]
      }
    ]
  },

    "member_checkins": {
    "label": "ประวัติการเข้าใช้",
    "api": "/api/member-checkins",
    "idKey": "checkin_id",

    "search": [
      {
        "key": "member_name",
        "label": "สมาชิก",
        "type": "text"
      }
    ],

    "form": [
      {
        "key": "member_id",
        "label": "สมาชิก",
        "type": "select",
        "optionsFrom": {
          "api": "/api/members",
          "value": "member_id",
          "label": "name"
        }
      },
      {
        "key": "checkin_time",
        "label": "เวลาเข้าใช้",
        "type": "datetime-local"
      },
      {
        "key": "checkout_time",
        "label": "เวลาออก (เว้นว่างหากยังไม่ออก)",
        "type": "datetime-local"
      }
    ]
  }
  
};

let current = Object.keys(ENTITIES)[0];
let editingId = null;
const $ = (s) => document.querySelector(s);
function setStatus(el, msg, cls = "") { el.className = "status " + cls; el.textContent = msg; }
async function api(url, opts) { const res = await fetch(url, opts); return res.json(); }

function fieldHtml(f, prefix, value = "") {
  // แปลงวันที่และเวลาให้แสดงในช่อง datetime-local
  if (f.type === "datetime-local" && value) {
    value = String(value).replace(" ", "T").slice(0, 16);
  }
  if (f.type === "heading") return '<div class="form-section">' + f.label + '</div>';
  let input;
  if (f.type === "select") {
    // options เป็นข้อความ "a" หรือ {value, label} ก็ได้
    input = '<select id="' + prefix + f.key + '">' +
      f.options.map(o => {
        const v = typeof o === "object" ? o.value : o;
        const t = typeof o === "object" ? o.label : (o || "ทั้งหมด");
        return '<option value="' + v + '"' + (String(v) === String(value ?? "") ? " selected" : "") + '>' + t + '</option>';
      }).join("") + '</select>';
  } else { input = '<input id="' + prefix + f.key + '" type="' + f.type + '" value="' + (value ?? "") + '">'; }
  return '<div class="field"><label>' + f.label + '</label>' + input + '</div>';
}
// ช่อง select ที่มี optionsFrom → ดึงตัวเลือกจาก API (เช่น รายชื่อหมวดหมู่จากฐานข้อมูล)
async function loadOptions(fields, forSearch) {
  for (const f of fields.filter(f => f.optionsFrom)) {
    const src = f.optionsFrom, r = await api(src.api);
    f.options = r.ok ? (r.data || []).map(row => ({ value: row[src.value], label: row[src.label] }))
                     : [{ value: "", label: (r.todo ? "🚧 " : "⚠️ ") + r.error }];
    if (forSearch && r.ok) f.options.unshift({ value: "", label: "ทั้งหมด" });
  }
}
// ช่องในฟอร์มที่ใช้อยู่ตอนนี้ (ช่อง editOnly แสดงเฉพาะตอนแก้ไข)
function formFields() { return ENTITIES[current].form.filter(f => !f.editOnly || editingId !== null); }
async function buildSearch() {
  const cfg = ENTITIES[current];
  await loadOptions(cfg.search, true);
  if (cfg !== ENTITIES[current]) return;   // ผู้ใช้เปลี่ยนแท็บระหว่างรอ
  $("#searchTitle").textContent = cfg.label;
  $("#searchFields").innerHTML = cfg.search.map(f => fieldHtml(f, "s_")).join("");
}
async function doSearch() {
  const cfg = ENTITIES[current];
  const params = new URLSearchParams();
  cfg.search.forEach(f => { const v = $("#s_" + f.key).value; if (v) params.append(f.key, v); });
  setStatus($("#status"), "กำลังค้นหา...");
  renderTable(await api(cfg.api + "?" + params.toString()));
}
function renderTable(r) {
  const head = $("#tableHead"), body = $("#tableBody"), st = $("#status");
  head.innerHTML = ""; body.innerHTML = "";
  if (!r.ok) { setStatus(st, (r.todo ? "🚧 " : "⚠️ ") + r.error, r.todo ? "todo" : "err"); return; }
  const rows = r.data || [];
  if (rows.length === 0) { setStatus(st, "ไม่พบข้อมูล"); return; }
  setStatus(st, "พบ " + rows.length + " รายการ");
  const cols = Object.keys(rows[0]);
  head.innerHTML = cols.map(c => {
  const label = entityColumnLabels[current]?.[c] || columnLabels[c] || c;
  return "<th>" + label + "</th>";
}).join("") + "<th>จัดการ</th>";
  body.innerHTML = rows.map(row => {
  const id = row[ENTITIES[current].idKey];

  return "<tr>" + cols.map(c => {
    let value = row[c] ?? "—";

    // แปลงสถานะการจองเป็นภาษาไทย
    if (c === "status") {
      value = statusLabels[value] || value;
    }

    return "<td>" + value + "</td>";
  }).join("") +
    '<td><button class="btn sm" onclick="editRow(' + id + ')">แก้ไข</button> ' +
    '<button class="btn sm del" onclick="deleteRow(' + id + ')">ลบ</button></td></tr>';
}).join("");
}
async function openForm(title, data = {}) {
  await loadOptions(formFields(), false);
  $("#modalTitle").textContent = title;
  $("#formFields").innerHTML = formFields().map(f => fieldHtml(f, "f_", data[f.key])).join("");
  $("#modal").classList.remove("hidden");
}
function collectForm() { const d = {}; formFields().filter(f => f.key).forEach(f => d[f.key] = $("#f_" + f.key).value); return d; }
async function editRow(id) {
  const cfg = ENTITIES[current];
  const r = await api(cfg.api + "/" + id);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  editingId = id; openForm("แก้ไขข้อมูล", r.data);
}
async function deleteRow(id) {
  if (!confirm("ยืนยันการลบ?")) return;
  const r = await api(ENTITIES[current].api + "/" + id, { method: "DELETE" });
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  doSearch();
}
async function save() {
  const cfg = ENTITIES[current], data = collectForm();
  const opts = { method: editingId ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) };
  const r = await api(editingId ? cfg.api + "/" + editingId : cfg.api, opts);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  $("#modal").classList.add("hidden"); doSearch();
}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
  t.classList.add("active"); current = t.dataset.entity;
  buildSearch(); $("#tableHead").innerHTML = ""; $("#tableBody").innerHTML = "";
  setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');
}));
$("#btnSearch").onclick = doSearch;
$("#btnClear").onclick = () => buildSearch();
$("#btnAdd").onclick = () => { editingId = null; openForm("เพิ่มข้อมูลใหม่"); };
$("#btnSave").onclick = save;
$("#btnCancel").onclick = () => $("#modal").classList.add("hidden");
buildSearch();
setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');

// Real-time search: ประวัติการเข้าใช้ Fitness
document.addEventListener("input", function (event) {
  const target = event.target;

  if (
    !target ||
    !target.id ||
    !target.id.includes("member_name")
  ) {
    return;
  }

  // ค้นหาเฉพาะเมื่ออยู่ในแท็บประวัติการเข้าใช้
  if (typeof current === "undefined" ||
      current !== "member_checkins") {
    return;
  }

  // ใช้ระบบค้นหาเดิมเมื่อพิมพ์
  const searchButton = document.querySelector("#btnSearch");

  if (searchButton) {
    searchButton.click();
  }
});
