import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DmsDialogComponent } from './dms-dialog.component';

describe('DmsDialogComponent', () => {
  let component: DmsDialogComponent;
  let fixture: ComponentFixture<DmsDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DmsDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DmsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
