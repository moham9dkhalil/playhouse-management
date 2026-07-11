# Contributing to Play House Management System

## Code Style

### Python
- استخدم PEP 8
- 4 spaces للـ indentation
- استخدم type hints حيث الإمكان
- اسم الملفات: lowercase_with_underscores
- اسم الدوال والمتغيرات: lowercase_with_underscores
- اسم الفئات: PascalCase

```python
# Good
def calculate_session_cost(hours: float, rate: float) -> float:
    return hours * rate

# Bad
def CalculateSessionCost(h, r):
    return h * r
```

### API Naming
- استخدم lowercase مع hyphens للـ endpoints
- استخدم معايير REST الصحيحة
- استخدم الأفعال الصحيحة (GET, POST, PUT, DELETE)

```
GET    /api/v1/customers/           # List
POST   /api/v1/customers/           # Create
GET    /api/v1/customers/{id}       # Get one
PUT    /api/v1/customers/{id}       # Update
DELETE /api/v1/customers/{id}       # Delete
```

## Commit Messages

اتبع هذا الصيغة:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat`: ميزة جديدة
- `fix`: إصلاح خطأ
- `docs`: تحديث التوثيق
- `style`: تنسيق الكود
- `refactor`: إعادة بناء الكود
- `perf`: تحسين الأداء
- `test`: إضافة اختبارات
- `chore`: مهام روتينية

### مثال:
```
feat(devices): add maintenance scheduling

Added ability to schedule device maintenance
with automatic notifications.

Closes #123
```

## Pull Requests

1. **Branch Name**: `feature/description` أو `fix/description`
2. **صفة PR**: اشرح الغرض والتغييرات
3. **الاختبارات**: أضف اختبارات للميزات الجديدة
4. **التوثيق**: حدّث التوثيق إذا لزم الأمر

## Testing

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبار محدد
pytest tests/test_devices.py

# مع تقرير التغطية
pytest --cov=app tests/
```

## Code Review Checklist

- [ ] الكود يتبع أسلوب المشروع
- [ ] توجد اختبارات كافية
- [ ] التوثيق محدثة
- [ ] لا توجد مشاكل أمان
- [ ] الأداء مقبول
- [ ] الرسائل واضحة

## Development Setup

```bash
# Clone
git clone https://github.com/moham9dkhalil/playhouse-management.git
cd playhouse-management

# البيئة الافتراضية
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# المكتبات
pip install -r backend/requirements.txt

# التطبيق
cd backend
uvicorn app.main:app --reload
```

## Database Migrations (عند الحاجة)

```bash
# إنشاء migration
alembic revision --autogenerate -m "Add new table"

# تطبيق migrations
alembic upgrade head

# العودة للإصدار السابق
alembic downgrade -1
```

## Debugging

### استخدام print (في التطوير فقط)
```python
print(f"DEBUG: {variable}")
```

### استخدام logging (أفضل)
```python
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Debug info: {variable}")
logger.info("Operation completed")
logger.warning("Warning message")
logger.error("Error message")
```

## Performance Tips

1. استخدم eager loading للعلاقات
2. أضف indexes للأعمدة المستخدمة كثيرًا
3. استخدم pagination للقوائم الكبيرة
4. cache النتائج المتكررة
5. استخدم async حيث الإمكان

## Security

- لا تضع secrets في الكود
- استخدم environment variables
- validate جميع المدخلات
- استخدم prepared statements
- لا تكشف معلومات حساسة في الأخطاء

## Documentation

كل دالة يجب أن تحتوي على docstring:

```python
def create_device(device_data: PlaystationDeviceCreate, user_id: int) -> PlaystationDevice:
    """
    Create a new PlayStation device
    
    Args:
        device_data: البيانات المدخلة للجهاز
        user_id: معرف المستخدم الذي ينشئ الجهاز
    
    Returns:
        PlaystationDevice: الجهاز المنشأ
    
    Raises:
        ValueError: إذا كان هناك جهاز بنفس الرقم التسلسلي
    """
    # Implementation
    pass
```

## Contact

- 💬 Issues: استخدم GitHub Issues
- 💭 Discussions: استخدم GitHub Discussions
- 📧 Email: contact@playhouse.local

---

شكرًا لمساهمتك! 🎉
