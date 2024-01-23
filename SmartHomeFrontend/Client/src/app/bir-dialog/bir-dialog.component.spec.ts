import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BirDialogComponent } from './bir-dialog.component';

describe('BirDialogComponent', () => {
  let component: BirDialogComponent;
  let fixture: ComponentFixture<BirDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BirDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BirDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
