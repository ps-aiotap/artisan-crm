# Generated by Django 4.2.7 on 2025-07-11 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeloop_user_id', models.IntegerField(blank=True, help_text='Reference to StoreLoop User ID', null=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20)),
                ('company', models.CharField(blank=True, max_length=200)),
                ('role', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(choices=[('storeloop_order', 'StoreLoop Order'), ('whatsapp', 'WhatsApp'), ('email', 'Email'), ('upwork', 'Upwork'), ('referral', 'Referral'), ('manual', 'Manual Entry')], max_length=50)),
                ('summary', models.TextField(blank=True, help_text='AI-generated customer summary')),
                ('intent_classification', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'crm_customer_profile',
            },
        ),
        migrations.CreateModel(
            name='LeadStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(default='#6B7280', max_length=7)),
                ('is_active', models.BooleanField(default=True)),
                ('mode', models.CharField(choices=[('storeloop', 'StoreLoop'), ('aiotap', 'AioTap'), ('shared', 'Shared')], default='shared', max_length=20)),
            ],
            options={
                'db_table': 'crm_lead_stage',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('color', models.CharField(default='#3B82F6', max_length=7)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'crm_tag',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('next_followup', models.DateTimeField(blank=True, null=True)),
                ('followup_count', models.PositiveIntegerField(default=0)),
                ('ai_next_action', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artisan_crm.customerprofile')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artisan_crm.leadstage')),
            ],
            options={
                'db_table': 'crm_lead',
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('phone', 'Phone'), ('upwork', 'Upwork'), ('internal', 'Internal Note')], max_length=20)),
                ('direction', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound'), ('internal', 'Internal')], max_length=10)),
                ('content', models.TextField()),
                ('summary', models.TextField(blank=True)),
                ('intent', models.CharField(blank=True, max_length=100)),
                ('sentiment', models.CharField(blank=True, max_length=20)),
                ('external_id', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='artisan_crm.customerprofile')),
            ],
            options={
                'db_table': 'crm_interaction',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('message_template', models.TextField()),
                ('ai_variations', models.JSONField(blank=True, default=list)),
                ('is_active', models.BooleanField(default=True)),
                ('sent_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('target_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artisan_crm.leadstage')),
                ('target_tags', models.ManyToManyField(blank=True, to='artisan_crm.tag')),
            ],
            options={
                'db_table': 'crm_campaign',
            },
        ),
        migrations.CreateModel(
            name='CustomerTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artisan_crm.customerprofile')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artisan_crm.tag')),
            ],
            options={
                'db_table': 'crm_customer_tag',
                'unique_together': {('customer', 'tag')},
            },
        ),
    ]
