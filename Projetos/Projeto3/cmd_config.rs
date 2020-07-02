// ApplicationId da entidade, fornecida pela AMA
static APPLICATION_ID: &'static str = "b826359c-06f8-425e-8ec3-50a97a418916";



// Devolve APPLICATION_ID (fornecida pela AMA).
fn get_appid() -> &'static str {
	return APPLICATION_ID;
}
