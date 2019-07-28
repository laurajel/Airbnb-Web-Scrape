abnb = airbnb1

slr_rr = lm(rates ~ rental_reviews, data = abnb)
slr_fa = lm(rates ~ feat_amenities, data = abnb)
slr_hr = lm(rates ~ host_reviews, data = abnb)
slr_ra = lm(rates ~ rental_age, data = abnb)



summary(slr_rr)
summary(slr_fa)
summary(slr_hr)
summary(slr_ra)


mlr = lm(rates ~ rental_reviews + feat_amenities + host_reviews + rental_age, data = abnb)

summary(mlr)


